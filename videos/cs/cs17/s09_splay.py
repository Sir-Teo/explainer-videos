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
        dl = label(r"node 1: \ depth $4\to0$; \ node 3: \ depth $2\to3$", font_size=17, color=GREY_B).next_to(
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
            label(r"the accessed node rises; \ other path nodes can move down", font_size=21, color=YES),
            label(r"arbitrary initial tree: \ $O((m+n)\log(n+1))$ for $m$ accesses", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Sleator and Tarjan's splay tree stores no balance metadata. <bookmark mark='a'/> After an "
            "access it rotates the node to the root. A zig is one rotation when the parent is the root. "
            "<bookmark mark='b'/> In a zig-zig, node and parent face the same direction: rotate the "
            "grandparent, then the parent. <bookmark mark='c'/> In a zig-zag they bend: rotate the "
            "accessed node up twice. <bookmark mark='d'/> A single deep access can still take linear "
            "work. <bookmark mark='e'/> In this five-node example, two zig-zigs move node one from depth "
            "four to zero, but node three moves down from depth two to three. Splaying does not halve "
            "every path node's depth. <bookmark mark='f'/> A potential argument bounds a whole sequence. "
            "From an arbitrary initial tree we must include initial potential, giving order m plus n "
            "times log of n plus one for m accesses."
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
        head = label(r"The access lemma: \ actual cost plus change in potential", font_size=32).to_edge(UP, buff=0.3)
        premise = label(r"positive proof weights $w(x)>0$; \ subtree weight $s(x)$; \ $r(x)=\log_2 s(x)$",
                        font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.35)
        phi = MathTex(r"\Phi(T)=\sum_x \log_2 s(x)", font_size=35, color=LAM).next_to(premise, DOWN, buff=0.25)
        witness = grid_table([r"five-node example", r"before", r"after"], [
            [r"subtree sizes, \ nodes 1,2,3,4,5", r"$1,2,3,4,5$", r"$5,2,1,4,1$"],
            [r"potential $\Phi$", r"$\log_2 120$", r"$\log_2 40$"],
        ], widths=[5.1, 3.3, 3.3], row_h=0.56, font_size=21, mono_cols=(),
            colors=[[GREY_A, DATA, YES], [GREY_A, DATA, YES]]).next_to(phi, DOWN, buff=0.3)
        actual = MathTex(r"4+\Delta\Phi=4-\log_2 3\approx2.415", font_size=33,
                         color=HEAD).next_to(witness, DOWN, buff=0.25)
        lemma = MathTex(r"\widehat c(x)\le 3\bigl(r(\mathrm{root})-r(x)\bigr)+1"
                        r"=O\!\left(1+\log\frac{W}{w(x)}\right)", font_size=31,
                        color=YES).next_to(actual, DOWN, buff=0.3)
        notes = VGroup(
            label(r"double rotations: \ $\widehat c\le3\Delta r(x)$; \ a final zig needs the extra $+1$",
                  font_size=20, color=GREY_A),
            label(r"unit weights, arbitrary initial tree: \ $O((m+n)\log(n+1))$ total for $m$ accesses",
                  font_size=21, color=HEAD),
            label(r"frequency weights: \ keep zero-frequency keys positive; \ include initialization potential",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.28)
        with self.voiceover(
            "The proof uses actual work plus a change in potential. <bookmark mark='a'/> Give every node "
            "a strictly positive weight. Subtree weight is s, rank is its logarithm, and potential is the"
            " sum of those ranks. <bookmark mark='b'/> Revisit the five-node example with unit weights. "
            "Before splaying, subtree sizes multiply to one hundred and twenty. Afterward they multiply "
            "to forty. Four rotations therefore cost four minus log base two of three in amortized units,"
            " about two point four. <bookmark mark='c'/> For a double rotation, the case analysis bounds "
            "amortized cost by three times the accessed node's rank increase. A final single zig needs an"
            " extra one. <bookmark mark='d'/> Telescoping gives the access lemma: at most three times the"
            " initial root-to-node rank difference, plus one. With unit weights, arbitrary initial "
            "potential adds an n log n term to the total bound. <bookmark mark='e'/> Weights belong to "
            "the proof, so frequency-based positive weights yield static optimality with setup costs "
            "included. Never assign weight zero and take its logarithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(premise))
            vo.wait_until("a"); self.play(FadeIn(phi))
            vo.wait_until("b"); self.play(FadeIn(witness), FadeIn(actual))
            vo.wait_until("c"); self.play(FadeIn(notes[0]))
            vo.wait_until("d"); self.play(FadeIn(lemma), FadeIn(notes[1]))
            vo.wait_until("e"); self.play(FadeIn(notes[2]))
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
        tab = grid_table([r"access sequence", r"splay: \ visits + rotations", r"AVL: \ visited nodes", r"entropy (bits)"], rows,
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
            "Here are four finite access workloads on the same two thousand keys. <bookmark mark='a'/> "
            "Repeated sorted scans are inexpensive for the splay tree, consistent with the "
            "sequential-access theorem. <bookmark mark='b'/> On this uniform random workload it does more"
            " logical node work than AVL. That is a measured workload, not the worst possible sequence. "
            "<bookmark mark='c'/> Skewed and hot-key workloads favor adaptation. The table's splay "
            "counter counts node visits and rotations, whereas AVL counts visited nodes; neither is a "
            "count of every Python predicate or a wall-clock benchmark. <bookmark mark='d'/> Dynamic "
            "optimality asks for a constant comparison to the best offline binary-search-tree execution "
            "on every sequence, with model and setup conventions. Selected 2026 progress appears in the "
            "frontier chapter; it does not settle constant competitiveness."
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
