from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Heaps(VoiceoverScene):
    def construct(self):
        self.card()
        self.interface()
        self.fibonacci()
        self.measured()

    def card(self):
        card = chapter_card(10, r"Priority queues", r"How cheap can ``decrease a key'' be?", lit=(1987,),
                            extra=((1987, r"Fredman and Tarjan: \ Fibonacci heaps"),), part=PART)
        with self.voiceover("Chapter ten. Priority queues."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def interface(self):
        head = label(r"Insert, \ delete-min, \ decrease-key", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            [r"binary heap \ (Part 16)", r"$O(\log n)$", r"$O(\log n)$", r"$O(\log n)$"],
            [r"binomial heap \ (Vuillemin, \ 1978)", r"$O(1)$ am.", r"$O(\log n)$", r"$O(\log n)$"],
            [r"Fibonacci heap \ (1987)", r"$O(1)$ am.", r"$O(\log n)$ am.", r"$O(1)$ am."],
            [r"pairing heap \ (1986)", r"$O(1)$", r"$O(\log n)$ am.", r"variant/model dependent"],
        ]
        tab = grid_table([r"heap", r"insert", r"delete-min", r"decrease-key"], rows, widths=[4.6, 2.2, 2.6, 3.4],
                         row_h=0.6, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, GREY_A, NO], [WHITE, GREY_A, GREY_A, GREY_A],
                                 [LAM, YES, GREY_A, YES], [WHITE, GREY_A, GREY_A, HEAD]]).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"Dijkstra's shortest paths \ (Part 18): \ $n$ delete-mins, \ up to $m$ decrease-keys", font_size=22,
                  color=GREY_A),
            MathTex(r"O((m+n)\log n) \text{ with a binary heap} \quad\to\quad O(m + n \log n) \text{ with a Fibonacci "
                    r"heap}", font_size=30, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "A priority queue supports a precise operation set. <bookmark mark='a'/> Binary heaps have "
            "logarithmic worst-case insert, delete-min and decrease-key with handles. Lazy binomial "
            "variants and Fibonacci heaps offer amortized bounds. Fibonacci decrease-key is constant "
            "amortized time in the pointer model. Pairing-heap bounds depend on the exact variant and "
            "allowed operations; this table avoids combining them into one generic claim. <bookmark "
            "mark='b'/> On nonnegative-weight graphs, Dijkstra can perform a delete-min per reached "
            "vertex and relax many edges. <bookmark mark='c'/> Including isolated vertices and "
            "initialization, the usual bounds are order m plus n times log n with a binary heap, and m "
            "plus n log n with Fibonacci heaps. A dense graph makes the asymptotic difference more "
            "significant."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def fibonacci(self):
        head = label(r"Fibonacci heaps: \ a marked parent loses its second child", font_size=32).to_edge(UP, buff=0.3)
        def forest(after=False):
            pos = {1: [0, 1.7], 4: [-0.8, 0.7], 7: [-1.4, -0.3], 8: [-0.2, -0.3]}
            if after: pos = {1: [-1.5, 1.7], 4: [0, 1.7], 7: [1.5, 1.7], 8: [0, 0.7]}
            nodes = {k: VGroup(Circle(radius=0.25, stroke_color=HEAD if k == 4 else DATA,
                                      stroke_width=2, fill_color=BG, fill_opacity=1),
                               mono("0" if after and k == 7 else str(k), 18, WHITE)).move_to([*xy, 0])
                     for k, xy in pos.items()}
            links = [(4, 8)] if after else [(1, 4), (4, 7), (4, 8)]
            edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), buff=0.25,
                                  color=GREY_B, stroke_width=1.5) for a, b in links])
            mark = label(r"marked: \ lost one child earlier", font_size=17, color=HEAD).next_to(nodes[4], RIGHT, buff=0.12)
            return VGroup(edges, *nodes.values(), *([] if after else [mark]))
        before = forest().move_to([-3.7, 0.65, 0])
        after = forest(True).move_to([3.5, 0.65, 0])
        arrow = Arrow(before.get_right() + RIGHT * 0.1, after.get_left() - RIGHT * 0.1, color=CTRL, buff=0.1)
        action = label(r"decrease 7 to 0; \ cut 0, \ then cut marked 4", font_size=19, color=CTRL).next_to(arrow, DOWN, buff=0.18)
        rules = VGroup(
            label(r"insert: \ append a singleton root; \ delete-min: \ link equal-degree roots", font_size=22, color=DATA),
            label(r"decrease-key: \ cut only if heap order is violated; \ losing a second child triggers a cascade", font_size=21, color=LAM),
            MathTex(r"\Phi=\#\mathrm{roots}+2\#\mathrm{marked}:\quad 1+2(1)=3\ \longrightarrow\ 3+2(0)=3", font_size=30, color=HEAD),
            label(r"a degree-$k$ subtree includes its root: \ at least $F_{k+2}\ge\varphi^k$ nodes", font_size=21, color=YES),
            label(r"theoretical time assumes constant-time pointer cuts; \ our Python lists count key comparisons", font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.28)
        with self.voiceover(
            "The Fibonacci heap delays work, while marks limit damage to its trees. <bookmark mark='a'/> "
            "Insert adds a singleton root. Delete-min eventually links roots of equal degree. <bookmark "
            "mark='b'/> Here node four is marked because it lost one child earlier. Lower seven's key to "
            "zero: heap order is violated, so cut that node into the root list. <bookmark mark='c'/> Four"
            " has now lost its second child, so cut four too and clear its mark. Cuts can cascade upward."
            " A decrease that preserves heap order does not need a cut. <bookmark mark='d'/> The "
            "potential is the number of roots plus twice the number of marked nodes. In this example it "
            "stays three: two extra roots replace one mark. The invariant forces a degree-k subtree, "
            "including its root, to contain at least Fibonacci k plus two nodes. <bookmark mark='e'/> "
            "Logarithmic degrees and the potential yield the theoretical bounds with constant-time "
            "pointer operations. Our educational Python implementation uses lists; its key-comparison "
            "counts do not certify those time bounds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(before))
            vo.wait_until("a"); self.play(FadeIn(rules[0]))
            vo.wait_until("b"); self.play(FadeIn(action))
            vo.wait_until("c"); self.play(GrowArrow(arrow), FadeIn(after), FadeIn(rules[1]))
            vo.wait_until("d"); self.play(FadeIn(rules[2:4]))
            vo.wait_until("e"); self.play(FadeIn(rules[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("heaps")
        head = label(r"Dijkstra on random graphs, \ counted", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), words(r["m"]), words(r["decrease"]), words(r["binary"]), words(r["pairing"]),
                 words(r["fibonacci"])] for r in d["rows"]]
        tab = grid_table([r"vertices", r"edges", r"decrease-keys", r"binary", r"pairing", r"Fibonacci"], rows,
                         widths=[1.8, 1.8, 2.4, 2.0, 2.0, 2.0], row_h=0.5, font_size=20,
                         colors=[[WHITE, WHITE, HEAD, GREY_A, YES, LAM]] * len(rows)).next_to(head, DOWN, buff=0.6)
        sub = label(r"key comparisons in the heap", font_size=19, color=GREY_B).next_to(tab, UP, buff=0.12).align_to(
            tab, RIGHT)
        pts = VGroup(
            label(r"actual key comparisons on three graphs; \ distances independently checked with heapq",
                  font_size=21, color=GREY_A),
            label(r"comparison counts do not measure pointer/list costs: \ native studies report workload-dependent "
                  r"results \ (Larkin, \ Sen and Tarjan, \ 2014)", font_size=21, color=NO),
            label(r"the asymptotic winner is not always the fastest; \ the amortized bound matters on the "
                  r"inputs that need it", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "What do these three graphs show? <bookmark mark='a'/> We count key comparisons inside each "
            "educational heap and verify all shortest-path distances independently with a heapq "
            "implementation. The displayed comparison savings depend on the graph. <bookmark mark='b'/> "
            "Comparisons are not time. Python list removal and bookkeeping do not implement the "
            "constant-time pointer operations assumed by Fibonacci-heap theory. Published native heap "
            "studies also report workload-dependent outcomes; no universal fastest heap follows. "
            "<bookmark mark='c'/> Use theoretical bounds to understand scaling, then measure complete "
            "equivalent tasks on the workload and implementation that matter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(sub))
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
